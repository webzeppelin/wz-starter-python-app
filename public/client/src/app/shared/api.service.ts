import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';

import 'rxjs/Rx'
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

import { Configuration } from '../app.config';
import { ServerTime } from './api.model'

@Injectable()
export class ApiService {

    title:String = 'Angular 2';

    private actionUrl: string;
    private headers: Headers;

    constructor(private _http: Http, private _configuration: Configuration) {

        this.actionUrl = _configuration.ApiBaseUrl;

        this.headers = new Headers();
        this.headers.append('Content-Type', 'application/json');
        this.headers.append('Accept', 'application/json');
    }

    public getServerTime = (): Observable<ServerTime> => {
        return this._http.get(this.actionUrl + 'time')
            .map((response: Response) => <ServerTime>response.json())
            .catch(this.handleError);
    }

    private handleError(error: Response) {
        console.error(error);
        return Observable.throw(error.json().error || 'Server error');
    }
}
