#\!/bin/bash
# Fix CSS for dark mode only by removing light/dark mode references
sed -i 's/text-text-light dark:text-text-dark/text-text/g' src/css/styles.css
sed -i 's/text-primary-light dark:text-primary-dark/text-primary/g' src/css/styles.css
sed -i 's/bg-light-light dark:bg-light-dark/bg-light/g' src/css/styles.css
sed -i 's/bg-background-light dark:bg-background-dark/bg-background/g' src/css/styles.css
sed -i 's/border-border-light dark:border-border-dark/border-border/g' src/css/styles.css
sed -i 's/bg-primary-light dark:bg-primary-dark/bg-primary/g' src/css/styles.css
sed -i 's/shadow-card dark:shadow-card-dark/shadow-card/g' src/css/styles.css
sed -i 's/text-muted-light dark:text-muted-dark/text-muted/g' src/css/styles.css
sed -i 's/hover:text-primary-light dark:hover:text-primary-dark/hover:text-primary/g' src/css/styles.css
sed -i 's/dark://g' src/css/styles.css
sed -i 's/-light\//-/g' src/css/styles.css
sed -i 's/-dark\//-/g' src/css/styles.css
