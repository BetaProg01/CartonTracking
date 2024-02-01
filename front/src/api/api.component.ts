import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-websocket',
  templateUrl: './websocket.component.html',
  styleUrls: ['./websocket.component.css']
})
export class WebsocketComponent implements OnInit {
  socket: WebSocket;

  constructor() { 
    this.socket = new WebSocket('ws://localhost:8000/gps_data');
  }

  ngOnInit(): void {
    this.socket = new WebSocket('ws://localhost:8000/gps_data');

    this.socket.onmessage = (event) => {
      console.log('Message from server: ', event.data);
    };

    this.socket.onopen = (event) => {
      this.socket.send('Hello, server!');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error: ', error);
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed: ', event);
    };
  }
}