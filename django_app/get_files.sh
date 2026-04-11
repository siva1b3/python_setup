cd /app/python_setup/django_app && find . -maxdepth 2 -name "*.md" | sort | while read -r filepath; do
    echo "================================================================"
    echo "FILE: $filepath"
    echo "================================================================"
    echo ""
    cat "$filepath"
    echo ""
    echo ""
done > all_phases.md