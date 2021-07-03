import { Component, OnInit } from '@angular/core';
import { ProductsService } from "./products.service";
import { map } from "rxjs/operators";

@Component({
  selector: 'app-products',
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss']
})
export class ProductsComponent implements OnInit {
  readonly products$ = this.productsService.getProducts();
  readonly loading$ = this.products$.pipe(map(value => !value));
  constructor(private productsService: ProductsService) {
  }

  ngOnInit(): void {
  }

  readonly columns = ['name'];

}
