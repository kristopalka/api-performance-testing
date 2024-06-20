import http from 'k6/http';

export const options = {
    vus: 1,
    duration: '1s',
};


export default function () {
    http.get('http://10.0.0.1:8081/hello');
}
