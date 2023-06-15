// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// go vet && go run -ldflags="-X main.version=$(git describe --always --long --dirty)" . -shouldDebug true

package main

import (
	"crypto/rand"
	"flag"
	"fmt"
	"github.com/sirupsen/logrus"
	"io"
	"math/big"
	"os"
	"strings"
)

// Replaced with:
//   -ldflags="-X main.version=$(git describe --always --long --dirty)"
var version string = "undefined"
var release string = "undefined"
var shouldDebug bool = false
var log *logrus.Logger

func random_unicode(input string) string {

	var (
		builder strings.Builder
		unicode_mapping []rune
		len_dictionary int64
		n_bi *big.Int
		n_int64 int64
		unicode_rune rune
		err error
	)

	for _, rune := range(input) {
		unicode_mapping = mapping[rune]
		if unicode_mapping == nil {
			fmt.Fprintf(&builder, "%c", rune)
			continue
		}

		len_dictionary = int64(len(unicode_mapping))

		n_bi, err = rand.Int(rand.Reader, big.NewInt(len_dictionary))
		if err != nil {
			log.Fatal("Error during rand.Int: ", err)
			panic(err)
		}
		n_int64 = n_bi.Int64()

		unicode_rune = unicode_mapping[n_int64]

		log.Printf("%c, %v, %v, %v %c\n", rune, unicode_mapping, len_dictionary, n_int64, unicode_rune)

		fmt.Fprintf(&builder, "%c", unicode_rune)
	}

	return builder.String()

}

func main() {

	var (
		logMain *logrus.Logger = &logrus.Logger{
			Out: os.Stderr,
			Formatter: new(logrus.TextFormatter),
			Level: logrus.DebugLevel,
		}
		ptrShouldDebug *string
		args []string
		input string
		output string
		out io.Writer
	)

	ptrShouldDebug = flag.String("shouldDebug", "false", "Should output debug output")

	flag.Parse()
	args = flag.Args()

	switch strings.ToLower(*ptrShouldDebug) {
	case "true":
		shouldDebug = true
	case "false":
		shouldDebug = false
	default:
		logMain.Fatal(fmt.Sprintf("Error: shouldDebug is not true/false (%s)\n", *ptrShouldDebug))
	}

	if shouldDebug {
		out = os.Stderr
	} else {
		out = io.Discard
	}
	log = &logrus.Logger{
		Out: out,
		Formatter: new(logrus.TextFormatter),
		Level: logrus.DebugLevel,
	}

	log.Printf("flag.Args = %v\n", args)
	if len(args) == 1 {
		input = args[0]
	} else if len(args) != 0 {
		logMain.Fatal(fmt.Sprintf("Error: Only one argument is allowed\n"))
	}

	log.Printf("version = %v\nrelease = %v\n", version, release)

	output = random_unicode(input)

	fmt.Printf("%s\n", output)

	os.Exit(0)
}
