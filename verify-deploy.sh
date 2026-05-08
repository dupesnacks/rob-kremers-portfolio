#!/bin/bash
# Pre-deploy verification script
# Checks that vercel.json routing points to files that actually exist

echo "🔍 Pre-deploy verification..."
echo ""

ERRORS=0

# Check critical routes
check_route() {
    local route="$1"
    local expected_file="$2"
    local full_path="/Users/rk/clawd$expected_file"
    
    if [ ! -f "$full_path" ]; then
        echo "❌ MISSING: $route → $expected_file"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
    
    # Check if vercel.json has correct routing
    if grep -q "\"source\": \"$route\"" /Users/rk/clawd/vercel.json; then
        if grep -A 1 "\"source\": \"$route\"" /Users/rk/clawd/vercel.json | grep -q "\"destination\": \"$expected_file\""; then
            echo "✅ $route → $expected_file"
            return 0
        else
            echo "⚠️  ROUTING MISMATCH: $route in vercel.json doesn't point to $expected_file"
            ERRORS=$((ERRORS + 1))
            return 1
        fi
    else
        echo "⚠️  $route not found in vercel.json"
        return 1
    fi
}

# Critical routes to verify
check_route "/teslasales" "/rob-kremers-portfolio/teslasales/index.html"
check_route "/r2" "/rob-kremers-portfolio/r2/index.html"
check_route "/rork" "/rork.html"
check_route "/rork2" "/rork2.html"
check_route "/flavorgalaxy" "/flavorgalaxy/index.html"

echo ""

if [ $ERRORS -gt 0 ]; then
    echo "❌ VERIFICATION FAILED ($ERRORS issues found)"
    echo "   Fix vercel.json or missing files before deploying."
    exit 1
else
    echo "✅ All verifications passed - safe to deploy"
    exit 0
fi
