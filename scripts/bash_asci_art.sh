mona_lisa=$(cat <<'EOF'
          ____
        o8%8888,
      o88%8888888.
     8'-    -:8888b
    8'         8888
   d8.-=.  ==-.:888b
   >8 '~'  '~'  d8888
   88      \    ,88888
   88b.  -~   ':88888
   888b ~==~ .:88888
   88888o--:':::8888
   88888| :::' 8888b
   8888^^'       8888b
  d888           ,%888b.
 d88%            %%%8--'-.
/88:.__ ,       _%-' ---  -
    '''::===..-'   =  --.
EOF
)

other_art=$(cat <<'EOF'
******  ,--./,-.
*****  / #      \
***   |   P*     |
*****  \   I    / 
******  `._,.P.+' 
EOF
)


# A prompt for activating Conda
read -p "Activate Conda base? (y/n): " activate_conda
if [[ $activate_conda == 'y' || $activate_conda == 'Y' ]]; then
    # Check if Conda is installed
    if command -v conda >/dev/null 2>&1; then
        # Conda is installed, activate it
        echo "$mona_lisa"
        #eval "$(command conda shell.bash hook 2> /dev/null)"
    else
        # Conda is not installed, display a message
        echo "Conda is not installed, use PIP."
    fi
else
    echo "$other_art"
fi