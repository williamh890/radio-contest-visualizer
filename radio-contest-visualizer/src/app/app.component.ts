import * as L from 'leaflet';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'app-root',
    template: `
        <app-map
            [sectors]="sectorsGet"
        >
        ></app-map>
    `,
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    public sectorsGet;

    constructor(private httpClient: HttpClient) {
    }

    ngOnInit() {
        this.sectorsGet = this.httpClient.get('assets/state.json')
            .map(s => {
                console.log(s);
                return s;
            });
    }
}
