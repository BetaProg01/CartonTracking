// app.component.ts
import { Component, ElementRef, ViewChild, Renderer2, OnInit } from '@angular/core';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
    @ViewChild('canvas', { static: true }) canvas!: ElementRef<HTMLCanvasElement>;
    X1!: number;
    Y1!: number;
    X2!: number;
    Y2!: number;
    X3!: number;
    Y3!: number;
    pixelColorArray1: number[][] = [];
    pixelColorArray2: number[][] = [];
    pixelColorArray3: number[][] = [];
    constructor(private renderer: Renderer2) {}
    ngOnInit(): void {
      console.log("coucou")
      const fileName = 'map.png'; // Specify the filename here
      const imageUrl = this.getImageUrl(fileName);
      this.loadImage(imageUrl); // Specify the filename here
    }
  
    loadImage(imageUrl: string): void {
      const image = new Image();
      image.onload = () => this.drawImage(image);
      image.src = imageUrl;
    }
  
    drawImage(image: HTMLImageElement): void {
      const canvas = this.canvas.nativeElement;
      const context = canvas.getContext('2d');
      if (context) {
        canvas.width = image.width;
        canvas.height = image.height;
  
        context.drawImage(image, 0, 0, image.width, image.height);
      this.control(context);
      
      } else {
        console.error('Canvas context is null.');
      }
      
    }
    getImageUrl(fileName: string): string {
      // Return the URL/path of the image file
      return `assets/${fileName}`; // Adjust the path if needed
    }
  
    dataURItoFile(dataURI: string, fileName: string): File {
      const byteString = atob(dataURI.split(',')[1]);
      const ab = new ArrayBuffer(byteString.length);
      const ia = new Uint8Array(ab);
      for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }
      return new File([ab], fileName, { type: 'image/png' }); // Adjust the type if needed
    }

    async control(context:CanvasRenderingContext2D){
      this.updateDots(context,1100,1000);
      setTimeout(() => { this.updateDots(context,1050,1000); }, 2000);
      setTimeout(() => { this.updateDots(context,1000,1000); }, 4000);
      setTimeout(() => { this.updateDots(context,1000,1050); }, 6000);
      setTimeout(() => { this.updateDots(context,1000,1100); }, 8000);
    }
    updateDots(context: CanvasRenderingContext2D, x1:number, y1:number){
      if (this.X3){
        this.eraseDot(context);
      }
      if (this.X2){
        this.X3 = this.X2;
        this.Y3 = this.Y2;
        this.putDot(context,this.X3,this.Y3,1,3);
      }
      if (this.X1){
        this.X2 = this.X1;
        this.Y2 = this.Y1;
        this.putDot(context,this.X2,this.Y2,1,4);
      }
      this.X1= x1;
      this.Y1 = y1;
      const imageData = context.getImageData(this.X1, this.Y1, 11, 11);
      const data = imageData.data;
      this.pixelColorArray3=[];
      this.pixelColorArray3=this.pixelColorArray2;
      this.pixelColorArray2=[];
      this.pixelColorArray2=this.pixelColorArray1;
      this.pixelColorArray1=[];
      // Store the color of each pixel in the pixelColorArray
      for (let i = 0; i < data.length; i += 4) {
        const pixelColor: number[] = [
          data[i],     // Red
          data[i + 1], // Green
          data[i + 2], // Blue
          data[i + 3]  // Alpha (fully opaque)
        ];
        this.pixelColorArray1.push(pixelColor);
      }
      this.putDot(context,x1,y1,1,5);
    }

    eraseDot(context :CanvasRenderingContext2D){
      const imageData = context.getImageData(this.X3, this.Y3, 11, 11);
      const newdata = imageData.data;
      console.log(this.pixelColorArray3);
      for (let i = 0, j = 0; i < newdata.length; i += 4, j++) {
        const pixelColor = this.pixelColorArray3[j];
        newdata[i] = pixelColor[0];     // Red
        newdata[i + 1] = pixelColor[1]; // Green
        newdata[i + 2] = pixelColor[2]; // Blue
        newdata[i + 3] = pixelColor[3]; // Alpha (fully opaque)
      }
      context.putImageData(imageData, this.X3, this.Y3);
    }

    putDot(context: CanvasRenderingContext2D, x:number, y:number, traveler:number, color:number){
      const imageData = context.getImageData(x, y, 11, 11); // Get pixel data for a 3x3 block starting at (100, 100)
      const data = imageData.data;
      if (traveler==1){
      for (let i = 0; i < data.length; i += 4) {
        data[i] = color*50;   // Red
        data[i + 1] = 0; // Green
        data[i + 2] = 0; // Blue
        data[i + 3] = 255; // Alpha (fully opaque)
      }
    } else {
      for (let i = 0; i < data.length; i += 4) {
        data[i] = 0;   // Red
        data[i + 1] = color*50; // Green
        data[i + 2] = 0; // Blue
        data[i + 3] = 255; // Alpha (fully opaque)
      }
    }
      context.putImageData(imageData, x, y); // Put modified pixel data back onto the canvas
    }
  }
