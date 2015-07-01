(function() {

	// Main entry point that gets included in index.html
	// checks for node-webkit before requirejs pipeline.

	// CHECKING FOR NODE-WEBKIT...
	// solves name-conflict with require statement from requirejs
	if (window && window.require) {
		require.nodeRequire = window.requireNode;
		console.log("app.js (node-webkit): initializing nw.gui");
		var nwgui = require('nw.gui');
		window.nwgui = nwgui;

		console.log("app.js (node-webkit): storing window");
		window.nwWindow = nwgui.Window.get();

		console.log("app.js (node-webkit): moving require to requirenw");
		window.requirenw = window.require;
		delete window.require;
		window.requirenw.version = process.versions.node;
		delete process.versions.node;
	}

	// START REQUIRE JS PIPELINE...
	console.log("app.js: initializing requirejs main.js");
	var script = document.createElement("script");
	script.type = "text/javascript";
	script.setAttribute("data-main", "build/prod"); // main entry point requirejs
	script.src = "bower_components/requirejs/require.js"; // link to require.js
	document.body.appendChild(script);

}());
