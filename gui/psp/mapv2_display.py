#!/usr/bin/python

import re

def escape_quotes_function(str_text): return re.sub(r'\'', "\\'", str_text)

def str_airport_and_city(apt, city_name, escape_quotes=False):
	if escape_quotes: city_name = escape_quotes_function(city_name)
	out_city_name = ''
	if city_name != 'NA': out_city_name = ' (' + city_name + ')'
	return '%s%s' % (apt, out_city_name)

def create_marker(apt, lat, lon, city_name):
	str_text = '<p style="font-size:small;">%s<br>lat: %.2f<br>lon: %.2f</p>' % (str_airport_and_city(apt, city_name, escape_quotes=True), lat, lon)
	return {'lat': lat, 'lon': lon, 'text': str_text}
		
def create_msg_coordinates(apt, city_name): return str_airport_and_city(apt, city_name) + '<br>'

def create_msg_distance(list_distances, list_airports, list_cities):
	msg = str_airport_and_city(list_airports[0], list_cities[0])
	total_d = 0
	for d, airport, city in zip(list_distances, list_airports[1:], list_cities[1:]):
		total_d += d
		msg += ' --- %d km --- %s' % (d, str_airport_and_city(airport, city))
	if len(list_distances) > 1: msg += ' ------------ total: %d km<br>' % total_d
	return msg
	
def create_points_around(coord):
	str_text = ''
	for delta_lat in [-5,5]:
		new_lat = max(min(coord['lat'] + delta_lat, 90), -90)
		for delta_lon in [-5,5]:
			new_lon = coord['lon'] + delta_lon
			str_text += 'var tmp = new GLatLng(%f,%f);\n' % (new_lat, new_lon)
			str_text += 'latlngbounds.extend( tmp );\n'
	return str_text

def create_html(google_key, list_markers, list_polylines, width=800, height=500, zoom=None, zoom_adjust=0, autocenter=True):
	# create head
	head = '<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;sensor=false&amp;key=%s" type="text/javascript"></script>' % google_key
	
	# body declaration
	body_declaration = '<body onunload="GUnload()">'
	
	# start script
	start_script = '<script type="text/javascript"> \n \
	//<![CDATA[ \n \
	if (GBrowserIsCompatible()) {  \n \
	// A function to create the marker and set up the event window \n \
	// Dont try to unroll this function. It has to be here for the function closure \n \
	// Each instance of the function preserves the contends of a different instance \n \
	// of the "marker" and "html" variables which will be needed later when the event triggers. \n \
	function createMarker(point,html) { \n \
	var marker = new GMarker(point); \n \
	GEvent.addListener(marker, "click", function() { \n \
	marker.openInfoWindowHtml(html); \n \
	}); \n \
	// The new marker "mouseover" listener \n \
        GEvent.addListener(marker,"mouseover", function() { \n \
          marker.openInfoWindowHtml(html); \n \
        }); \n \
	return marker; \n \
	}\n'
    
    # map_html
	map_html = '<div id="map" style="width: %dpx; height: %dpx"></div>\n' % (width, height)
    
    # initialize map
	initialize_map = 'var map = new GMap2(document.getElementById("map")); \n \
	map.addControl(new GLargeMapControl()); \n \
	map.addControl(new GMapTypeControl()); \n \
	map.enableScrollWheelZoom(); \n \
	var latlngbounds = new GLatLngBounds( );\n'
    
    # create markers
	create_markers = ''
	for marker in list_markers:
		create_markers += 'var point = new GLatLng(%f,%f);\n' % (marker['lat'], marker['lon'])
		create_markers += 'latlngbounds.extend( point );\n'
		create_markers += 'var marker = createMarker(point,\'<div style="width:240px">%s<\/div>\');\n' % marker['text']
		create_markers += 'map.addOverlay(marker);\n'
		create_markers += create_points_around(marker)
	
	# create lines
	create_lines = ''
	for line in list_polylines:
		create_lines += 'var polyOptions = {geodesic:true};\n'
		create_lines += 'var point1 = new GLatLng(%f,%f);\n' % (line['1']['lat'], line['1']['lon'])
		create_lines += 'var point2 = new GLatLng(%f,%f);\n' % (line['2']['lat'], line['2']['lon'])
		create_lines += 'var polyline = new GPolyline([ point1, point2 ], "%s", %d, 1, polyOptions);\n' % (line['color'], line['width'])
		create_lines += 'map.addOverlay(polyline);\n'
		create_lines += create_points_around(line['1'])
		create_lines += create_points_around(line['2'])
	
	# center and zoom
	if zoom is None: zoom = 'map.getBoundsZoomLevel( latlngbounds ) + (%d)' % zoom_adjust
	center_and_zoom = 'map.setCenter( latlngbounds.getCenter( ),  %s );\n' % zoom
	
	# end script
	end_script = '}\n \
    \n \
    // display a warning if the browser was not compatible \n \
    else { \n \
      alert("Sorry, the Google Maps API is not compatible with this browser"); \n \
    } \n \
    </script>\n'
	
	# create map (concatenate previous)
	create_map = start_script + initialize_map + create_markers + create_lines + center_and_zoom + end_script
	
	return head, body_declaration, map_html, create_map