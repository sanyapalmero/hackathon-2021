import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  constructor(private http: HttpClient) {
  }

  public url = 'api'

  getProducts(): Observable<ReadonlyArray<Product>> {
    return this.http.get<ReadonlyArray<Product>>(this.url + 'api/products/');
  }
}

export interface Product {
  id: string,
  name: string,
  offer_set: any,
  keywords: string
}
