import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";
import { LazyLoadEvent } from "primeng/api";

@Injectable({
  providedIn: 'root'
})
export class ProductsService {

  constructor(private http: HttpClient) {
  }

  public url = 'api'

  getProducts(event: LazyLoadEvent): Observable<{ count, results: ReadonlyArray<Product> }> {
    let filters = {
      name__icontains: event.filters["name__icontains"]?.value?event.filters["name__icontains"].value:'',
      offers__name__icontains: event.filters["event.offers__name__icontains"]?.value?event.filters["event.offers__name__icontains"].value:'',
      resource_code__icontains: event.filters["resource_code__icontains"]?.value?event.filters["resource_code__icontains"]?.value:''
    }
    let params = {
      page_size: event.rows.toString(),
      page: (Math.round(event.first/event.rows)+1).toString(),
      ...filters
    }
    return this.http.get<any>(this.url + 'api/products/', {
      params
    })
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<any>(this.url + 'api/products/' + id + '/');
  }

  getOffers(id: any) {
    return this.http.get<any>(this.url + 'api/offers/', {
      params: {
        product__id: id,
        page_size: 999
      }
    });
  }
}

export interface Product {
  id: string,
  name: string,
  offer_set: any,
  keywords: string
}
