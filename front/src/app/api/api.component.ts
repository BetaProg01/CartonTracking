import { Component, OnInit } from '@angular/core';
import { DataTransferService } from '../service/data-transfer.service';

@Component({
  selector: 'app-websocket',
  templateUrl: './api.component.html',
  styleUrls: ['./api.component.css']
})
export class WebsocketComponent implements OnInit {
  socket!: WebSocket;
  private address = 'ws://localhost:8000/gps_data';
  private connectionInterval;

  constructor(private dataTransferService: DataTransferService) {
    this.connectionInterval = setInterval(() => {
      if (!this.socket || this.socket.readyState === WebSocket.CLOSED) {
        this.socket = new WebSocket(this.address);
        this.initializeWebSocket();
      }
    }, 10000); // Try to connect every 10 seconds
  }

  ngOnInit(): void {
    console.log("Starting websocket component")
  }

  initializeWebSocket(): void {
    this.socket.onmessage = (event) => {
      console.log('Message from server: ', event.data);
      const data = JSON.parse(event.data);  // Parse the JSON string to an object
      const key = data.key; // This the number of the traveler (1 or 2 in theory)
      const date = data.date;
      const x_pos = data.x_pos;
      const y_pos = data.y_pos; 
      this.dataTransferService.updateData(x_pos, y_pos, key);
    };

    this.socket.onopen = (event) => {
      this.socket.send('Hello, server!');
      console.log('Started connection to websocket');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error: ', error);
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed: ', event);
    };
  }
}