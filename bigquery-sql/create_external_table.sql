-- Create a new table fraud_dataset_final from external table:
Create or replace table `suryo-df8.final_project.fraud_dataset_final`
as
select * from `suryo-df8.final_project.external_table`
order by datetime ASC;

create or replace table `suryo-df8.final_project.fraud_dataset_final` as
  select extract(date from datetime) as date, 
  step, type,
  amount,
  nameOrig as senderID,
  oldbalanceOrg as oldbalanceSend,
  newbalanceOrig as newbalanceSend,
  abs(newbalanceOrig-oldbalanceOrg) as difsender,
  nameDest as ReceiverID,
  oldbalanceDest as oldbalancereceive,
  newbalanceDest as newbalancereceive,
  abs(newbalanceDest-oldbalanceDest) as difreceiver,
  isFraud,
  isFlaggedFraud,
  datetime,
  extract(time from datetime) as time
  from `suryo-df8.final_project.external_table`
  order by datetime ASC;
