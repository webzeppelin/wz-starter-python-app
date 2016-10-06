import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';

import 'rxjs/Rx'
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

import { Configuration } from '../app.config';
import { ServerTime, GuestbookEntry, GuestbookEntrySet } from './api.model'

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

    public signGuestbook = (entry: GuestbookEntry): Observable<GuestbookEntry> => {
        // post to the API with the supplied entry
        console.log("Would have posted to guestbook API");
        return Observable.of(new GuestbookEntry(666, entry.name, entry.message, new Date()));
    }

    public browseGuestbook = (): Observable<GuestbookEntrySet> => {
        // retrieve the most recent guestbook entries
        console.log("Would have returned the most recent guestbook entries");
        let fake_entries: GuestbookEntry[] = [
            new GuestbookEntry(1, 'Andy Ford', 'This is my first time signing the guest book.', new Date()),
            new GuestbookEntry(2, 'Andy Ford', 'I could not help but sign this thing again.', new Date())
        ];
        return Observable.of(
            new GuestbookEntrySet(fake_entries, fake_entries.length, 2, true)
        );
    }

    public browseGuestbookMore = (last_id: number): Observable<GuestbookEntrySet> => {
        // retrieve the most recent guestbook entries
        console.log('Would have returned entries older than '+last_id);
        let fake_entries: GuestbookEntry[] = [
            new GuestbookEntry(3, 'Franky Mo', 'I want to do this, too!', new Date()),
            new GuestbookEntry(4, 'Franky Mo', 'I am back for more.', new Date())
        ];
        return Observable.of(
            new GuestbookEntrySet(fake_entries, fake_entries.length, 4, false)
        );
    }

    private handleError(error: Response) {
        console.error(error);
        return Observable.throw(error.json().error || 'Server error');
    }
}
