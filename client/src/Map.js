import ReactDOM from 'react-dom';
import React from 'react';
import App from "./App";

//open layers and styles
var ol = require('openlayers');
require('openlayers/css/ol.css');

class Map extends React.Component {

    componentDidMount() {

        // create feature layer and vector source
        var featuresLayer = new ol.layer.Vector({
            source: new ol.source.Vector({
                features:[]
            })
        });

        // create map object with feature layer
        alert('tonio')
        var map = new ol.Map({
            target: this.refs.mapContainer,
            layers: [
                //default OSM layer
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                }),
                featuresLayer
            ],
            view: new ol.View({
                center: [-11718716.28195593, 4869217.172379018], //Boulder
                zoom: 13,
            })
        });

        map.on('click', this.handleMapClick.bind(this));

        // save map and layer references to local state
        this.setState({
            map: map,
            featuresLayer: featuresLayer
        });

    }

    // pass new features from props into the OpenLayers layer object
    componentDidUpdate(prevProps, prevState) {
        this.state.featuresLayer.setSource(
            new ol.source.Vector({
                features: this.props.routes
            })
        );
    }

    handleMapClick(event) {

        // create WKT writer
        var wktWriter = new ol.format.WKT();

        // derive map coordinate (references map from Wrapper Component state)
        var clickedCoordinate = this.state.map.getCoordinateFromPixel(event.pixel);

        // create Point geometry from clicked coordinate
        var clickedPointGeom = new ol.geom.Point( clickedCoordinate );

        // write Point geometry to WKT with wktWriter
        var clickedPointWkt = wktWriter.writeGeometry( clickedPointGeom );

        // place Flux Action call to notify Store map coordinate was clicked
        // Actions.setRoutingCoord( clickedPointWkt );
        //

    }

    render () {
        return (
            <div ref="mapContainer"> </div>
        );
    }

}

export default Map;