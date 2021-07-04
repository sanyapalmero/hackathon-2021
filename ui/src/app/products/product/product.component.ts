import { Component, OnInit } from '@angular/core';
import { ProductsService } from "../products.service";
import { ActivatedRoute } from "@angular/router";
import { switchAll, switchMap } from "rxjs/operators";

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss']
})
export class ProductComponent implements OnInit {

  constructor(private service: ProductsService,
              private route: ActivatedRoute) {
  }

  data$ = this.route.params.pipe(switchMap(params => this.service.getProduct(params['id'])));

  ngOnInit(): void {
  }

}
