# Maintainer: Andre Blanke

pkgname='terrariad'
pkgver='1.0.1'
pkgrel=1
pkgdesc='Terraria server daemon providing socket activation'
arch=('any')
url='https://github.com/andreblanke/terrariad'
license=('MIT')
depends=('python')
source=("https://github.com/andreblanke/$pkgname/archive/refs/tags/v$pkgver.zip")
sha256sums=('2c509d6c2b76e2985eba63e7da09c0312b73fcc7783edb991b7862e0bdfe2f37')

package() {
    cd "$pkgname-$pkgver"

    install -D --mode=755 'terrariad.py'      "$pkgdir/usr/bin/terrariad"
    install -D --mode=644 'terrariad.service' "$pkgdir/usr/lib/systemd/system/terrariad.service"
    install -D --mode=644 'LICENSE.txt'       "$pkgdir/usr/share/licenses/terrariad/LICENSE.txt"
}
