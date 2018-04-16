import React, { PropTypes } from "react";

import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-15';

configure({ adapter: new Adapter() });

import { shallow } from "enzyme";
import { Results } from "../../components/results";

import fetchMock from 'fetch-mock'
import endpointJSON from '../utils'


const mockReturnJSON = endpointJSON('hmis_only', 'jurisdictional_roles.json')
fetchMock.getOnce(
  '/api/upload/jurisdictional_roles.json',
  {
    body: mockReturnJSON,
    headers: { 'content-type': 'application/json' }
  }
)
describe("Results", () => {
  let props;
  let mountedResultsPage;
  const resultsPage = () => {
    if (!mountedResultsPage) {
      mountedResultsPage = shallow(
        <Results {...props} />
      );
    }
    return mountedResultsPage;
  }

  beforeEach(() => {
    props = {
      updateMatchingResults: jest.fn(),
      handleControlledDate: jest.fn(),
      nextPage: jest.fn(),
      prevPage: jest.fn(),
      updateDates: jest.fn(),
      updateTableSort: jest.fn(),
      filteredData: {
        tableData: [],
        jailDurationBarData: [],
        homelessDurationBarData: [],
        jailContactBarData: [],
        homelessContactBarData: []
      },
      filters: {
        controlledDate: '',
        startDate: '',
        endDate: '',
        limit: 20,
        offset: 0,
        orderColumn: 'matched_id',
        order: 'asc',
        setStatus: 'All'
      },
      vennDiagramData: [{sets: [''], size: null}, {sets: [''], size: null}, {sets: [''], size: null}],
      currentPage: 0,
    };
    mountedResultsPage = undefined;
  });
  
  describe('Table#onNextPageClick', () => {
    it("fires off nextPage", () => {
      props.totalTableRows = 10
      props.filteredData.tableData = [
        [{name: 'Dr. Teeth'}],
        [{name: 'Animal'}],
        [{name: 'Floyd Pepper'}],
        [{name: 'Janice'}],
        [{name: 'Zoot'}],
        [{name: 'Lips'}]
      ]
      const wrapper = resultsPage()
      wrapper.find('DataTables').simulate('nextPageClick')
      expect(props.nextPage.mock.calls.length).toBe(1);
    });
  });

  describe('Table#onSortOrderChange', () => {
    it("fires off updateTableSort", () => {
      props.totalTableRows = 10
      props.filteredData.tableData = [
        [{name: 'Dr. Teeth'}],
        [{name: 'Animal'}],
        [{name: 'Floyd Pepper'}],
        [{name: 'Janice'}],
        [{name: 'Zoot'}],
        [{name: 'Lips'}]
      ]
      const wrapper = resultsPage()
      wrapper.find('DataTables').simulate('sortOrderChange', ['name', 'desc'])
      const callback = props.updateTableSort
      expect(callback.mock.calls.length).toBe(1);
      expect(callback.mock.calls[0]).toEqual([['name', 'desc']])
    });
  });

  describe('DatePicker#onChange', () => {
    it("fires off updateDates", () => {
      const wrapper = resultsPage()
      const callback = props.updateDates
      wrapper.find('DatePicker').simulate('change', null, new Date(2016, 0, 1))
      expect(callback.mock.calls[1]).toEqual(['2015-01-01', '2016-01-01'])
    });
  });
});
