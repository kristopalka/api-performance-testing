import http from 'k6/http';

export const options = {
    scenarios: {
        ramping: {
            executor: 'ramping-arrival-rate',
            startRate: __ENV.START_RPS,
            timeUnit: '1s',
            preAllocatedVUs: __ENV.ALLOCATED_VUS,
            stages: [
                { target: __ENV.END_RPS, duration: `${__ENV.DURATION}s` },
            ],
        },
    },
};

export default function () {
    http.get(__ENV.URL);
}


