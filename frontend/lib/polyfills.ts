// Polyfill for Promise.withResolvers (Node.js < 22 / older browsers)
// This must be imported before any library that uses Promise.withResolvers

if (typeof Promise.withResolvers === 'undefined') {
  // @ts-expect-error polyfill
  Promise.withResolvers = function <T>() {
    let resolve: (value: T | PromiseLike<T>) => void;
    let reject: (reason?: unknown) => void;
    const promise = new Promise<T>((res, rej) => {
      resolve = res;
      reject = rej;
    });
    return { promise, resolve: resolve!, reject: reject! };
  };
}

export {};
