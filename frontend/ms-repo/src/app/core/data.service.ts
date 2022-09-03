import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { NgxSpinnerService } from 'ngx-spinner';
import { Subject } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
};

@Injectable({
  providedIn: 'root',
})
export class DataService {
  public locationReady = new Subject<boolean>();
  map_config: any = {
    key: 'AIzaSyB5fQm8qdSuEpSbl7NrhLObmrN-g61kVo4',
  };
  teams: any;
  taskTypes: any;
  clients: any;
  // serverUrl = 'http://localhost:8080'; //local setting
  serverUrl = ''; //production setting
  clientLocation: any;
  teamLocation: any;
  constructor(private http: HttpClient, private spinner: NgxSpinnerService) {
  }
  load(): any {
    return new Promise((resolve, reject) => {
      this.http
        .get(this.serverUrl + '/clients', httpOptions)
        .subscribe((result) => {
          this.clients = result;
        });
      this.http
        .get(this.serverUrl + '/types', httpOptions)
        .subscribe((result) => {
          this.taskTypes = result;
          resolve(true);
        });
    });
  }

  getTeams(filterCriteria: any): any {
    this.spinner.show();
    this.http
      .post(this.serverUrl + '/predict', filterCriteria)
      .subscribe((value: any) => {
        this.teams = value;
        this.spinner.hide();
      });
  }

  /**
   * Uses the Google Geocoding API to fetch lat and long of a location
   *
   * @param {location} location Location for which geo location is to be extracted.
   *
   * @memberOf DataService
   */
  fetchGeoLocation(location1: string, location2: string): any {
    let url1 =
      'https://maps.googleapis.com/maps/api/geocode/json?address=' +
      location1 +
      '&key=' +
      this.map_config.key;
    let url2 =
      'https://maps.googleapis.com/maps/api/geocode/json?address=' +
      location2 +
      '&key=' +
      this.map_config.key;
    this.http.get(url1, {}).subscribe((result: any) => {
      this.clientLocation = result.results[0].geometry.location;
      this.http.get(url2, {}).subscribe((result: any) => {
        this.teamLocation = result.results[0].geometry.location;
        this.locationReady.next(true);
      });
    });
  }
}
