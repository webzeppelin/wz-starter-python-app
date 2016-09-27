import { Component, Input, OnInit } from '@angular/core';
import { ServerTime } from '../api.model'
import { ApiService } from '../api.service'

@Component({
  selector: 'clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.scss']
})
export class ClockComponent implements OnInit {

    server_time: ServerTime;

    constructor(private api: ApiService) {
        // Do something with api
    }

    observeServerTime(): void {
        this.api.getServerTime()
            .subscribe(
                st => this.setServerTime(st),
                error => console.error('Error: ' + error),
                () => console.log('Completed!')
            )
    }

    setServerTime(st: ServerTime): void {
        this.server_time = st;
    }

    ngOnInit() {
        this.observeServerTime();
    }
}