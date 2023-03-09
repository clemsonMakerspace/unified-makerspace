
// This function must be run as a Google Apps Script (currently being run from a student's account - potentially could move to Makerspace's google account)

// Must first install S3 Library from: https://engetc.com/projects/amazon-s3-api-binding-for-google-apps-script/

// Can be automatically executed on a schedule using "Triggers" in Apps Script


// This function gathers data from a Google sheet and puts a csv in a specified S3 bucket
function uploadToS3() {

  // Get the data from the Google Sheet - Replace SheetID and SheetName (Not the name of the sheets document, but the actual sheet tab name - located at the bottom of Google Sheets document) 
  var sheetId = '<YOUR_SHEET_ID>';
  var sheetName = '<YOUR_SHEET_NAME>';
  var sheet = SpreadsheetApp.openById(sheetId).getSheetByName(sheetName);
  
  fileName = sheet.getName() + ".csv";

  // convert all available sheet data to csv format
  var csvFile = convertRangeToCsvFile_(fileName, sheet);
  
  //Third party library named S3 is used to send data to S3.

  // replace with your own IAM User's access key and secret access key
  // This IAM role should preferably only have access to your one target S3 bucket
  var s3 = S3.getInstance("<AWS_ACCESS_KEY>", "<AWS_SECRET_KEY>");

  // edit with your S3 bucket name and your filename that will be uploaded
  s3.putObject("<YOUR_S3_BUCKET_NAME>", "<YOUR_FILENAME>.csv", csvFile, {logRequests:true});


 
}

// Converts DataRange object to a CSV
function convertRangeToCsvFile_(csvFileName, sheet) {
  // get available data range in the spreadsheet
  var activeRange = sheet.getDataRange();
  try {
    var data = activeRange.getValues();
    var csvFile = undefined;

    // Replaces any spaces in headers with underscores
    var headers = data[0];
    for (var i = 0; i < headers.length; i++) {
      headers[i] = headers[i].toString().replace(/\s+/g, '_');
    }
    data[0] = headers;

    // loop through the data in the range and build a string with the csv data
    if (data.length > 1) {
      var csv = "";
      for (var row = 0; row < data.length; row++) {
        for (var col = 0; col < data[row].length; col++) {
          if (data[row][col].toString().indexOf(",") != -1) {
            data[row][col] = "\"" + data[row][col] + "\"";
          }
        }

        // join each row's columns
        // add a carriage return to end of each row, except for the last one
        if (row < data.length-1) {
          csv += data[row].join(",") + "\r\n";
        }
        else {
          csv += data[row];
        }
      }
      csvFile = csv;
    }
    return csvFile;
  }
  catch(err) {
    Logger.log(err);
    Browser.msgBox(err);
  }
}