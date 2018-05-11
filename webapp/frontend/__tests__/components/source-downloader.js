import React, { PropTypes } from "react";

import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-15';

configure({ adapter: new Adapter() });

import { shallow } from "enzyme";
import { SourceDownloader } from "../../components/source-downloader";

describe("SourceDownloader", () => {
  let props;
  let mountedSourceDownloader;
  const sourceDownloader = () => {
    if (!mountedSourceDownloader) {
      mountedSourceDownloader = shallow(
        <SourceDownloader {...props} />
      );
    }
    return mountedSourceDownloader;
  }

  beforeEach(() => {
    props = {
      availableEventTypes: [],
    };
    mountedSourceDownloader = undefined;
  });
  describe('SourceDownloadButtons', () => {
    it("displays each authorized event type in a dropdown and allow download", () => {
      props.availableEventTypes = [
        {name: 'Jail Bookings', slug: 'jail_bookings'},
        {name: 'Booking Charges', slug: 'jail_booking_charges'}
      ]
      const wrapper = sourceDownloader()
      const callback = jest.fn()
      wrapper.instance().downloadSource = callback
      wrapper.find('SelectField').simulate('change', null, null, 'jail_booking_charges')
      wrapper.find('RaisedButton').simulate('click')
      expect(callback.mock.calls.length).toBe(1)
      expect(callback.mock.calls[0]).toEqual(['jail_booking_charges'])
    });
  });
});
