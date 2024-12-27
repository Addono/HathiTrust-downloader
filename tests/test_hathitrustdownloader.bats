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

@test "Download using a complete URL" {
  run hathitrust-downloader "https://babel.hathitrust.org/cgi/pt?id=mdp.39015027794331&seq=1" 1 1 --name "$TMP_DIR/test_url_page"
  [ "$status" -eq 0 ]
  [ -f "$TMP_DIR/test_url_page_p000000.pdf" ]
}
