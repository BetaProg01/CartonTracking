// data_transfer.service.ts
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataTransferService {
  private data = new BehaviorSubject<{x_pos: number, y_pos: number, traveler: number}>({x_pos: 0, y_pos: 0, traveler: 0});
  currentData = this.data.asObservable();

  constructor() { }

  updateData(x_pos: number, y_pos: number, traveler: number) {
    this.data.next({x_pos, y_pos, traveler});
    console.log("Updating data: ", x_pos, y_pos, traveler);
  }
}