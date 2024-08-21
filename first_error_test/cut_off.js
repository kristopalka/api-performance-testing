import http from 'k6/http';
import {Counter} from 'k6/metrics';

const failed = new Counter('failed_counter');

export const options = {
    scenarios: {
        test: {
            executor: 'constant-arrival-rate',
            rate: __ENV.RPS,
            timeUnit: '1s',
            duration: `${__ENV.DURATION}s`,
            preAllocatedVUs: __ENV.ALLOCATED_VUS,
        },
    },
    thresholds: {
        'failed_counter{scenario:test}': [{
            threshold: 'count<1',
            abortOnFail: true,
            delayAbortEval: '0s'
        }]
    },
};

export default function () {
    let timestamp_start = new Date().toISOString();

    const r = http.get(__ENV.URL);

    if (r.error_code === 0) {
        failed.add(0, {timestamp_start: timestamp_start})
    } else {
        failed.add(1, {timestamp_start: timestamp_start})
    }
}


