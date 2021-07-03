import { Injectable } from '@angular/core';

@Injectable({providedIn: 'root'})
export class LocalStorage implements Storage {

  get length(): number {
    return window.localStorage.length;
  }

  clear(): void {
    return window.localStorage.clear();
  }

  getItem(key: string): string | null {
    return window.localStorage.getItem(key);
  }

  key(index: number): string | null {
    return window.localStorage.key(index);
  }

  removeItem(key: string): void {
    const event = new StorageEvent('storage', {
      key,
      newValue: undefined,
      oldValue: window.localStorage.getItem(key),
    });
    setTimeout(() => window.dispatchEvent(event), 0);
    return window.localStorage.removeItem(key);
  }

  setItem(key: string, value: string): void {
    const event = new StorageEvent('storage', {
      key,
      newValue: value,
      oldValue: window.localStorage.getItem(key),
    });
    setTimeout(() => window.dispatchEvent(event), 0);
    return window.localStorage.setItem(key, value);
  }

  [name: string]: any;

}