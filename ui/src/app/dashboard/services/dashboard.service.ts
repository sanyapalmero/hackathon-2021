import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  constructor(private http: HttpClient) {
  }

  public url = 'api'

  getData(): Observable<any> {
    return this.http.get(this.url + 'api/products/')
  }
}
