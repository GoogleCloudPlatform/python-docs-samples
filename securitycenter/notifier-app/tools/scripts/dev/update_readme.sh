#!/bin/bash

main() {

for i in $(find tools/scripts -name *.sh  | egrep -v '(dev|lib)' | sort); do
  echo "" >> README.md;
  echo "## $i" >> README.md;
  echo "" >> README.md;
  echo "\`\`\`" >> README.md;
  $i -h 2>> README.md;
  echo "\`\`\`" >> README.md;
done

}

main "$@"
