#!/bin/bash
# Script to run screenshot generation in batches

# Navigate to project root
cd "$(dirname "$0")/../.."

# Total number of links (this is an estimate, the actual count may vary)
TOTAL_LINKS=200

# Number of links to process per run
BATCH_SIZE=20

# Loop through the batches
for ((i=0; i<$TOTAL_LINKS; i+=$BATCH_SIZE))
do
  echo "------------------------------------------------"
  echo "Processing batch starting at index $i (size $BATCH_SIZE)"
  echo "------------------------------------------------"
  node scripts/screenshots/generate-screenshots-batch.js $i $BATCH_SIZE
  
  # Wait a few seconds between batches
  echo "Waiting 5 seconds before starting next batch..."
  sleep 5
done

echo "All batches completed!"