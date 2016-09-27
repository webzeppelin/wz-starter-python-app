import { Injectable } from '@angular/core';

@Injectable()
export class Configuration {
    public ApiServer: string = "http://localhost:8081/";
    public ApiBasePath: string = "api/v1/";
    public ApiBaseUrl: string = this.ApiServer + this.ApiBasePath;
}