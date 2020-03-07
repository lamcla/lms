import { requestConfig } from './methods';

describe('postmessage_json_rpc/methods', () => {
  describe('requestConfig', () => {
    let configEl;

    beforeEach('inject the client config into the document', () => {
      configEl = document.createElement('script');
      configEl.setAttribute('type', 'application/json');
      configEl.classList.add('js-config');
      configEl.textContent = JSON.stringify({
        hypothesisClient: { foo: 'bar' },
      });
      document.body.appendChild(configEl);
    });

    afterEach('remove the client config from the document', () => {
      configEl.parentNode.removeChild(configEl);
    });

    it('returns the config object', () => {
      assert.deepEqual(requestConfig(), { foo: 'bar' });
    });
  });

  describe('readyToReceive', () => {});
});
