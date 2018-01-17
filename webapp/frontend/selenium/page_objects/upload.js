var uploadCommands = {
  uploadGoodHMIS: function() {
    return this
      .setValue(
        'input[type="file"]',
        require('path').resolve(__dirname + '/../../../sample_data/uploader_input/hmis-fake-0.csv'),
        function(result) { if(result.status != 0) { console.log(result) } }
      )
      .waitForElementVisible('@upload', 1000)
      .click('@upload')
  },
  uploadBadHMIS: function() {
    return this
      .setValue(
        'input[type="file"]',
        require('path').resolve(__dirname + '/../../../sample_data/uploader_input/hmis-bad-0.csv'),
        function(result) { if(result.status != 0) { console.log(result) } }
      )
      .waitForElementVisible('@upload', 1000)
      .click('@upload')
  },
  uploadGoodBookings: function() {
    return this
      .setValue(
        'input[type="file"]',
        require('path').resolve(__dirname + '/../../../sample_data/uploader_input/bookings-fake-0.csv'),
        function(result) { if(result.status != 0) { console.log(result) } }
      )
      .waitForElementVisible('@upload', 1000)
      .click('@upload')
  },
}
module.exports = {
  commands: [uploadCommands],
  elements: {
    hmisStays: { 
      selector: "//span[text()='HMIS Service Stays']",
      locateStrategy: 'xpath'
    },
    jailBookings: { 
      selector: "//span[text()='Jail Bookings']",
      locateStrategy: 'xpath'
    },
    browseForFile: {
      selector: "//span[text()='Browse for File']",
      locateStrategy: 'xpath'
    },
    upload: {
      selector: "//span[contains(text(), '.csv')]",
      locateStrategy: 'xpath'
    },
    uploadConfirmButton: {
      selector: "//button[contains(., 'Confirm Upload')]",
      locateStrategy: 'xpath'
    },
    tryAgainButton: {
      selector: "//span[text()='Try Again']",
      locateStrategy: 'xpath'
    },
    backToHomeButton: {
      selector: "//button[contains(., 'Back to Home')]",
      locateStrategy: 'xpath'
    }
  }
};
