import { Component, OnInit } from '@angular/core';
import { ProductsService } from "../products.service";
import { Route } from "@angular/router";

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss']
})
export class ProductComponent implements OnInit {

  constructor(private service: ProductsService,
              private route: Route) { }
  data$ = this.service
  ngOnInit(): void {
  }

}
