import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  constructor(private http: HttpClient) {
  }

  public url = 'api'

  getProducts(page: number,
              size: number, search?: { [key: string]: string }): Observable<{ count, results: ReadonlyArray<Product> }> {
    let params = {
      page_size: size.toString(),
      page: (page + 1).toString(),
      ...search
    }
    return this.http.get<any>(this.url + 'api/products/', {
      params
    })
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<any>(this.url + 'api/products/' + id + '/');
  }
}

export interface Product {
  id: string,
  name: string,
  offer_set: any,
  keywords: string
}
