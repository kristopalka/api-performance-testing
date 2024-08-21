import http from 'k6/http';
import {Trend} from 'k6/metrics';

const stats = new Trend('http_req_stats');

export const options = {
    scenarios: {
        constant: {
            executor: 'constant-arrival-rate',
            rate: __ENV.RPS,
            timeUnit: '1s',
            duration: `${__ENV.DURATION}s`,
            preAllocatedVUs: __ENV.ALLOCATED_VUS,
        },
    },
};

export default function () {
    let timestamp_start = new Date().toISOString();

    const r = http.get(__ENV.URL);

    let timestamp_end = new Date().toISOString();

    stats.add(r.timings.duration + r.timings.blocked, {
        timestamp_start: timestamp_start,
        timestamp_end: timestamp_end,
        error: r.error_code,
        blocked: r.timings.blocked,
        connecting: r.timings.connecting,
        sending: r.timings.sending,
        waiting: r.timings.waiting,
        receiving: r.timings.receiving,
        duration: r.timings.duration,
    });
}


