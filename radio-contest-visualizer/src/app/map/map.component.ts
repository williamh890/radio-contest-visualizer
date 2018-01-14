import * as L from 'leaflet';

import { Component, OnInit, Input } from '@angular/core';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

export const mapOptions = {
    center: new L.LatLng(64.086251, -142.331676),
    zoom: 5,

    maxBounds: new L.LatLngBounds(
        new L.LatLng(-90, -300),
        new L.LatLng(90, 300)
    ),

    maxBoundsViscosity: 0.8,
    minZoom: 2.2,
    maxZoom: 15
};

@Component({
    selector: 'app-map',
    template: `
        <div id="map"></div>
    `,
    styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
    @Input() sectors: Observable<any>;

    private map: L.Map;

    constructor() { }

    ngOnInit() {
        this.map = new L.Map('map', mapOptions);

        L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(this.map);

        this.sectors.subscribe(sectors => {
            L.geoJSON(sectors).addTo(this.map);
        });
    }

}
