import http from 'k6/http';

export const options = {
    scenarios: {
        scenario: {
            executor: 'constant-arrival-rate',
            rate: __ENV.RPS,
            timeUnit: '1s',
            duration: `${__ENV.DURATION}s`,
            preAllocatedVUs: __ENV.ALLOCATED_VUS,
        },
    },
};

export default function () {
    http.get(__ENV.URL);
}


