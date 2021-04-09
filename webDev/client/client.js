

var net = require('net');
var http = require('http'); 
var client = new net.Socket();
const path = require('path')

var gui = require('/gui.html')



client.connect(1337, '127.0.0.1', function() {
	console.log('Connected');
	client.write('Hello, server! Love, Client.');
});

client.on('data', function(data) {
	console.log('Received: ' + data);
	client.destroy(); // kill client after server's response
});

client.on('close', function() {
	console.log('Connection closed');
});