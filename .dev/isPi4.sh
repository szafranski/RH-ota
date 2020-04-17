ifs=':' read -ra piversion <<< "$(cat /proc/cpuinfo | grep Revision)"
if [[ ${piversion[2]} == *"03111"*  ]] ; then
  echo "Pi 4 detected - no errors" || echo " -- error! -- "
else
  echo "This is not Pi 4 - no errors" || echo " -- error -- "
fi

echo "  Thanks Casey!  ￼ "
