import { Component, OnInit } from '@angular/core';

import OlMap from 'ol/Map';
import OlXYZ from 'ol/source/XYZ';
import OlTileLayer from 'ol/layer/Tile';
import OlView from 'ol/View';
import TileWMS from 'ol/source/TileWMS';
import {defaults as defaultControls, ScaleLine} from 'ol/control.js';
import { fromLonLat } from 'ol/proj';
import Geocoder from 'ol-geocoder'
@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})

export class MapComponent implements OnInit {

  map: OlMap;
  source: OlXYZ;
  layer: OlTileLayer;
  view: OlView;
  wms: OlTileLayer;

  ngOnInit() {
    // layers
    this.wms = new OlTileLayer({
      source: new TileWMS({
        url: 'http://localhost:8600/geoserver/wms',
        params: {'LAYERS': 'bd_topo_ign:arrondissement', 'TILED': true},
        serverType: 'geoserver',
        transition: 0
      })
    })
    this.source = new OlXYZ({
      url: 'http://tile.osm.org/{z}/{x}/{y}.png'
    });

    this.layer = new OlTileLayer({
      source: this.source
    });

    // map and view
    this.view = new OlView({
      center: fromLonLat([2.35, 48.85]),
      zoom: 11
    });

    this.map = new OlMap({
      controls: defaultControls().extend([
        new ScaleLine()
      ]),
      target: 'map',
      layers: [this.layer, this.wms],
      view: this.view
    });

    //controls
    let geocoder = new Geocoder('nominatim', {
      provider: 'osm',
      lang: 'fr-FR',
      autoComplete: true,
      autoCompleteMinLength: 3,
      placeholder: 'Osm serach ...',
      targetType: 'text-input',
      limit: 5,
      keepOpen: true
    });

    this.map.addControl(geocoder);
    geocoder.on('addresschosen', function(evt){
      let feature = evt.feature,
        coord = evt.coordinate,
        address = evt.address;
      // some popup solution
      //alert('zoomed to '+ coord)

    });
  }
}
