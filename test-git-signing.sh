#!/bin/bash

echo "Checking Git commit signing configuration..."

# Check if GPG key is properly configured
git_signing_key=$(git config --get user.signingkey)
if [ -z "$git_signing_key" ]; then
  echo "❌ No signing key configured"
else
  echo "✅ Signing key configured: $git_signing_key"
fi

# Check if commit signing is enabled
git_sign_commits=$(git config --get commit.gpgsign)
if [ "$git_sign_commits" != "true" ]; then
  echo "❌ Commit signing is not enabled"
else
  echo "✅ Commit signing is enabled"
fi

# Check if GPG program is configured
git_gpg_program=$(git config --get gpg.program)
if [ -z "$git_gpg_program" ]; then
  echo "ℹ️ No specific GPG program configured, using system default"
else
  echo "✅ GPG program configured: $git_gpg_program"
fi

# Test if GPG key is available
echo "Testing GPG key..."
gpg --list-secret-keys "$git_signing_key" > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "❌ GPG key not found or not accessible"
else
  echo "✅ GPG key is accessible"
fi

echo ""
echo "To test commit signing, try making a commit:"
echo "git commit --allow-empty -m \"Test signed commit\""
echo ""
echo "Then verify the commit is signed:"
echo "git log -1 --show-signature"
