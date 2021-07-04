import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProductsRoutingModule } from './products-routing.module';
import { ProductsComponent } from './products.component';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { ProductComponent } from './product/product.component';
import { TableModule } from "primeng/table";
import { CardModule } from "primeng/card";
import { DividerModule } from "primeng/divider";
import { OrderListModule } from "primeng/orderlist";
import { DataViewModule } from "primeng/dataview";


@NgModule({
  declarations: [
    ProductsComponent,
    ProductComponent
  ],
  imports: [
    CommonModule,
    ProductsRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    TableModule,
    CardModule,
    DividerModule,
    OrderListModule,
    DataViewModule
  ]
})
export class ProductsModule { }
