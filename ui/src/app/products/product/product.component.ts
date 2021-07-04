import { Component, OnInit } from '@angular/core';
import { ProductsService } from "../products.service";
import { ActivatedRoute } from "@angular/router";
import { map, switchMap } from "rxjs/operators";

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss']
})
export class ProductComponent implements OnInit {

  constructor(private service: ProductsService,
              private route: ActivatedRoute) {
  }

  id$ = this.route.params.pipe(map(params => params['id']));
  data$ = this.id$.pipe(switchMap(id => this.service.getProduct(id)));
  offers$ = this.id$.pipe(switchMap(id => this.service.getOffers(id)), map(({results}) => results));

  ngOnInit(): void {
  }

}
