#!/usr/bin/env bats

setup_file() {
  if [ -z "$BATS_TEST_TIMEOUT" ]; then
    export BATS_TEST_TIMEOUT=300
  fi
}

setup() {
  # Create a temporary directory for test files
  TMP_DIR=$(mktemp -d)
}

teardown() {
  # Remove the temporary directory
  rm -rf "$TMP_DIR"
}

@test "Check if hathitrust-downloader CLI is available" {
  run hathitrust-downloader --help
  [ "$status" -eq 0 ]
  [[ "$output" == *"usage: hathitrust-downloader"* ]]
}

@test "Download a single page" {
  run hathitrust-downloader mdp.39015027794331 1 1 --name "$TMP_DIR/test_single_page"
  [ "$status" -eq 0 ]
  [ -f "$TMP_DIR/test_single_page_p000000.pdf" ]
}

@test "Download multiple pages" {
  run hathitrust-downloader mdp.39015027794331 1 3 --name "$TMP_DIR/test_multiple_pages"
  [ "$status" -eq 0 ]
  [ -f "$TMP_DIR/test_multiple_pages_p000000.pdf" ]
  [ -f "$TMP_DIR/test_multiple_pages_p000001.pdf" ]
  [ -f "$TMP_DIR/test_multiple_pages_p000002.pdf" ]
}

@test "Handle invalid book ID" {
  run hathitrust-downloader invalid_id 1 1 --name "$TMP_DIR/test_invalid_id"
  [ "$status" -ne 0 ]
  [[ "$output" == *"An error occurred"* ]]
}

@test "Handle invalid page range" {
  run hathitrust-downloader mdp.39015027794331 10 1 --name "$TMP_DIR/test_invalid_range"
  [ "$status" -ne 0 ]
  [[ "$output" == *"An error occurred"* ]]
}
