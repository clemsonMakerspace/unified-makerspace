import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ModalService {
  constructor() {}

  modalStatus = new BehaviorSubject({
    open: false,
  });

  close(): void {
    this.modalStatus.next({
      open: false,
    });
  }

  open(): void {
    this.modalStatus.next({
      open: true,
    });
  }
}
