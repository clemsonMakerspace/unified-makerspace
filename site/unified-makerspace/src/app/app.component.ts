import {Component, HostListener,} from '@angular/core';
import {AuthService} from './shared/auth/auth.service';
import {environment} from '../environments/environment';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  constructor(public auth: AuthService) {
  }

  title = 'The MakerSpace';
  layerTransforms = this.positionFooter();

  get inProduction() {
    return environment.production;
  }

  @HostListener('window:scroll', ['$event'])
  onScroll(e) {
    this.layerTransforms = this.positionFooter();
  }

  positionFooter() {
    let percent = Math.pow(
      window.scrollY / (document.body.scrollHeight - window.innerHeight),
      2
    );
    let ranges = [
      [100, 170],
      [60, 100],
      [-20, 5],
    ];

    let base = 0;
    let positions = ranges.map((r) => base + r[0] + (r[1] - r[0]) * percent);
    return positions.map((p) => 'translateY(' + p + '%)');
  }
}
