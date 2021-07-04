import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { ProductsService } from "./products.service";
import { debounceTime, filter, map, share, startWith, switchMap, tap } from "rxjs/operators";
import { BehaviorSubject, combineLatest, Subject } from "rxjs";
import { FormControl, FormGroup } from "@angular/forms";
import { LazyLoadEvent } from "primeng/api";

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss'],
})
export class ProductsComponent implements OnInit {

  columns = ['name', 'measure_unit', 'resource_code', 'offers_count'];
  searchForm: { [key: string]: FormControl } = this.columns.reduce(
    (acc: { [key: string]: FormControl }, curr) => (
      acc[curr + '__icontains'] = new FormControl(''), acc)
    , {}
  );
  searchFormGroup = new FormGroup({
    'name__icontains': new FormControl(''),
    'offers__name__icontains': new FormControl(''),
    'resource_code__icontains': new FormControl('')
  });

  constructor(private productsService: ProductsService) {
  }

  lazy$ = new BehaviorSubject<LazyLoadEvent>(null);

  private request$ = this.lazy$.pipe(
    filter(query => !!query),
    tap(console.log),
    switchMap(query => this.productsService.getProducts(query)),
  );

  data$ = this.request$.pipe(
    map(({results}) => results),
    share(),
  );

  loading$ = this.data$.pipe(
    map(value => !value),
  );

  total$ = this.request$.pipe(
    map(({count}) => count),
    startWith(1),
  );

  ngOnInit(): void {
  }
}
