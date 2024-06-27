import http from 'k6/http';

export const options = {
};


export default function () {
    http.get(__ENV.URL);
}


