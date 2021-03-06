import {Component, DoCheck, HostListener, OnChanges, SimpleChanges} from '@angular/core';
import {AuthService} from './shared/auth/auth.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent{

  constructor(public auth: AuthService) {}



  title = 'The MakerSpace';
  layerTransforms = this.positionFooter();

  @HostListener('window:scroll', ['$event'])
  onScroll(e) {
    this.layerTransforms = this.positionFooter();
  }


  positionFooter() {
    let base = 0;
    let percent = Math.pow(window.scrollY / (document.body.scrollHeight - window.innerHeight), 2);
    let ranges = [[100, 170], [60, 100], [0, 0]];
    let positions = ranges.map(r => base + r[0] + (r[1] - r[0])*percent)
    return positions.map(p => 'translateY(' + p + '%)');

  }


}
