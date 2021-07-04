import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { ProductsService } from "./products.service";
import { debounceTime, filter, map, share, startWith, switchMap, tap } from "rxjs/operators";
import { combineLatest, Subject } from "rxjs";
import { isPresent, tuiReplayedValueChangesFrom } from "@taiga-ui/cdk";
import { FormControl, FormGroup } from "@angular/forms";

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss'],
})
export class ProductsComponent implements OnInit {

  readonly columns = ['name', 'measure_unit', 'resource_code', 'offers_count'];
  searchForm: { [key: string]: FormControl } = this.columns.reduce(
    (acc: { [key: string]: FormControl }, curr) => (
      acc[curr+'__icontains'] = new FormControl(''), acc)
    , {}
  );
  searchFormGroup = new FormGroup({
    'name__icontains': new FormControl(''),
    'offers__name__icontains': new FormControl(''),
    'resource_code__icontains': new FormControl('')
  });

  constructor(private productsService: ProductsService) {
  }

  private readonly size$ = new Subject<number>();
  private readonly page$ = new Subject<number>();
  private readonly request$ = combineLatest([
    this.page$.pipe(startWith(0)),
    this.size$.pipe(startWith(10)),
    tuiReplayedValueChangesFrom<{ [key: string]: string }>(this.searchFormGroup)
  ]).pipe(
    switchMap(query => this.productsService.getProducts(...query).pipe(
      startWith(null)
    )),
    share(),
  );
  readonly loading$ = this.request$.pipe(
    map(value => !value),
  );
  readonly total$ = this.request$.pipe(
    filter(isPresent),
    map(({count}) => count),
    startWith(1),
  );
  readonly data$ = this.request$.pipe(
    filter(isPresent),
    map(({results}) => results),
    map(products => products.filter(isPresent)),
    startWith([]),
  );

  ngOnInit(): void {
  }

  onSize(size: number) {
    this.size$.next(size);
  }

  onPage(page: number) {
    this.page$.next(page);
  }
}
